import { useState } from 'react'
import './App.css'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [fileName, setFileName] = useState('No file chosen')

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result.split(',')[1])
      reader.onerror = (error) => reject(error)
    })
  }

  const handleImageUpload = async (event) => {
    const file = event.target.files[0]
    if (file) {
      try {
        const base64Image = await convertToBase64(file)
        setSelectedImage(URL.createObjectURL(file))
        await sendToAPI(base64Image)
      } catch (err) {
        setError('Error processing image')
        console.error(err)
      }
    }
  }

  const sendToAPI = async (base64Image) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('http://localhost:5000/api/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'your-api-key-here' // Replace with your actual API key
        },
        body: JSON.stringify({ image: base64Image }),
      })
      
      if (!response.ok) {
        throw new Error('API request failed')
      }
      
      const data = await response.json()
      setPrediction(data.data)
    } catch (err) {
      setError('Error communicating with API')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Genshin Character Classifier</h1>
      
      <div className="upload-section">
        <label className="custom-file-input">
          <input
            type="file"
            accept="image/png, image/jpeg"
            onChange={handleImageUpload}
          />
          <div className="upload-button">Choose File</div>
        </label>
        <div className="file-name">{fileName}</div>
    </div>

      {error && <div className="error">{error}</div>}

      {selectedImage && (
        <div className="preview-section">
          <h2>Selected Image:</h2>
          <img src={selectedImage} alt="Preview" className="preview-image" />
        </div>
      )}

      {loading && <div className="loading">Processing...</div>}

      {prediction && (
        <div className="result-section">
          <h2>Prediction Result:</h2>
          <p>Character: {prediction.character}</p>
          <p>Confidence: {(prediction.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  )
}

export default App