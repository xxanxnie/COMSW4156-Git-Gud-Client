import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>GitGud Resource Services</h1>
      </header>

      <main>
        <h2>Resources at Various Locations</h2>

        {/* Embed Google Map */}
        <div className="map-container">
          <iframe
            title="GitGud Resource Services Map"  // Added title for accessibility
            src="https://www.google.com/maps/d/embed?mid=14XVnxzDNbzIQO4uYFbQNRypgUKFtXX0&ehbc=2E312F"
            width="1100"
            height="800"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
          ></iframe>
        </div>
      </main>
    </div>
  );
}

export default App;
