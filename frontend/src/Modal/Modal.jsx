import React from 'react';
import ReactDOM from 'react-dom';

import './styles.css';

const modalRoot = document.getElementById('modal-root');

class Modal extends React.Component {
  constructor(props) {
    super(props);
    this.el = document.createElement('div');
  }

  componentDidMount() {
    modalRoot.appendChild(this.el);
  }

  componentWillUnmount() {
    modalRoot.removeChild(this.el);
  }

  render() {
    const modal = (
      <div className="modal-container">
        <div className="modal">
          <div className="close" onClick={() => this.props.toggleModal()}>close</div>
          {this.props.children}
        </div>
      </div>
    );
    return ReactDOM.createPortal(
      modal,
      this.el,
    );
  }
}

export default Modal;