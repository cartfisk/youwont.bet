import React, { Component } from 'react';
import './App.css';

import ImageUpload from './ImageUpload/ImageUpload';
import Modal from './Modal/Modal';
import { SlotMachine } from './SlotMachine/SlotMachine';

import audio from './sound/audio.mp3';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uploadSuccessful: false,
      uploadModalOpen: false
    }
    this.uploadSuccess = this.uploadSuccess.bind(this)
    this.toggleModal = this.toggleModal.bind(this)
    this.download = this.download.bind(this);
  }

  toggleModal() {
    this.setState({ uploadModalOpen: !this.state.uploadModalOpen });
  }

  uploadSuccess() {
    this.setState({uploadSuccessful: true});
  }

  download() {

  }
  
  render() {
    const uploadDisabled = false;
    const downloadDisabled = !this.state.uploadSuccessful;
    const modal = this.state.uploadModalOpen ? (
      <Modal
        toggleModal={this.toggleModal}
      >
        <ImageUpload
          disabled={uploadDisabled}
          onConfirm={this.toggleModal}
          onSuccess={this.uploadSuccess}
        />
      </Modal>
    ) : null;
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
              <button className="top-buttons blue" id="left-button" onClick={() => this.toggleModal()}>
                BET
              </button>
              {modal}
              <button className={`top-buttons ${downloadDisabled ? 'disabled' : 'green'}`} id="right-button" style={{disabled: true}}>
                CASH OUT
              </button>
              <button className="bottom-button yellow">
                CREDITS
              </button>
            </div>
          </div>
        </div>
        <div style={{display: "none"}}>
          <audio controls autoPlay>
            <source src={audio} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      </div>
    );
  }
}

export default App;
