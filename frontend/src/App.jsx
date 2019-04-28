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
      uploadModalOpen: false,
      successModalOpen: false,
    }
    this.uploadSuccess = this.uploadSuccess.bind(this)
    this.toggleUploadModal = this.toggleUploadModal.bind(this)
    this.toggleSuccessModal = this.toggleSuccessModal.bind(this)
    this.download = this.download.bind(this);
  }

  toggleUploadModal() {
    this.setState({ uploadModalOpen: !this.state.uploadModalOpen });
    this.setState({ successModalOpen: this.state.uploadModalOpen });
  }
  toggleSuccessModal() {
    this.setState({ successModalOpen: !this.state.successModalOpen });
  }

  uploadSuccess() {
    this.setState({uploadSuccessful: true});
  }

  download() {

  }
  
  render() {
    const uploadDisabled = false;
    const downloadDisabled = !this.state.uploadSuccessful;
    const uploadModal = this.state.uploadModalOpen ? (
      <Modal
        toggleModal={this.toggleUploadModal}
      >
        <ImageUpload
          disabled={uploadDisabled}
          onConfirm={this.toggleUploadModal}
          onSuccess={this.uploadSuccess}
        />
      </Modal>
    ) : null;
    const successModal = this.state.successModalOpen ? (
      <Modal
        toggleModal={this.toggleSuccessModal}
      >
        <div className="success">
          <h2>we got your drop</h2>
          <h3>thank you.</h3>
        </div>
      </Modal>
    ) : null;
    return (
      <div className="App">
        <div className="background">
          <div className="grid">
            <div className="slot-machine-graphic">
              <a className="album-art" href="https://youwont.bet/static/master.png"></a>
              <div className="reels-container">
                <SlotMachine />
              </div>
              <button className="top-buttons blue" id="left-button" onClick={() => this.toggleUploadModal()}>
                BET
              </button>
              {uploadModal}
              {successModal}
              <button className={`top-buttons ${downloadDisabled ? 'disabled' : 'green'}`} id="right-button" style={{disabled: true}}>
                CASH OUT
              </button>
              <button className="bottom-button yellow">
                CREDITS
              </button>
            </div>
          </div>
        </div>
        <audio src={audio} controls autoPlay style={{ display: "none" }}/>
      </div>
    );
  }
}

export default App;
