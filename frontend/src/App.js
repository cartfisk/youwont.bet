import React, { Component } from 'react';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <form method="post" enctype="multipart/form-data" action="/api/v1/upload">
          <input type="file" name="file" accept="image/*" />
          <input type="submit" value="Upload" />
        </form>
      </div>
    );
  }
}

export default App;
