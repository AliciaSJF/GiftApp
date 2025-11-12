import './VideoDemo.css'

const VideoDemo = () => {
  return (
    <section id="video-demo" className="video-demo">
      <div className="container">
        <h2 className="section-title">Vídeo Demo</h2>
        <p className="section-subtitle">
          Descubre cómo funciona Whisy en este vídeo demostrativo
        </p>
        <div className="video-wrapper">
          <iframe
            src="https://www.youtube.com/embed/4VWXtrW9VNw?si=py1v1pbdphv72ZKK"
            title="Whisy Demo"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="video-iframe"
          ></iframe>
        </div>
      </div>
    </section>
  )
}

export default VideoDemo

