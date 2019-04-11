import React, { Component } from 'react';
import './App.css';

import ImageUpload from './ImageUpload/ImageUpload';
import { SlotMachine } from './SlotMachine/SlotMachine';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uploadSuccessful: false
    }
    this.uploadSuccess = this.uploadSuccess.bind(this)
    this.download = this.download.bind(this);
  }

  uploadSuccess() {
    this.setState({uploadSuccessful: true});
  }
  download() {

  }
  
  render() {
    const uploadDisabled = false;
    const downloadDisabled = !this.state.uploadSuccessful;
    return (
      <div className="App">
        <div className="background">
          <div className="grid">
            <div className="slot-machine-graphic">
              <div className="album-art">
              </div>
              <div className="reels-container">
                <SlotMachine />
              </div>
              <ImageUpload
                disabled={uploadDisabled}
                onSuccess={this.uploadSuccess}
              />
              <button className={`top-buttons ${downloadDisabled ? 'disabled' : 'green'}`} id="right-button" style={{disabled: true}}>
                CASH OUT
              </button>
              <button className="bottom-button yellow">
                CREDITS
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
