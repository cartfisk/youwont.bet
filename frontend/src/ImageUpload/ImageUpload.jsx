import React from 'react';
import './styles.css';

class ImageUpload extends React.Component {
    constructor(props) {
        super(props);
    
        this.handleChange = this.handleChange.bind(this);
    }

    state = {
        uploading: false,
        images: [],
        value: null,
        file: null
    }
    
    handleChange(e) {
        e.preventDefault();

        const files = this.uploadInput.files;
        const data = new FormData();
        data.append('file', files[0]);

        this.setState({
            file: URL.createObjectURL(e.target.files[0]),
            fileData: data
        })
    }
    
    handleSubmit() {
        this.setState({ uploading: true })

        fetch('/api/v1/upload', {
            method: 'POST',
            body: this.state.fileData
        })
        .then(response => {
            response.json().then((body) => {
                this.setState({ uploading: false });
            });
        })
        this.props.onConfirm();
    }
    
    render() {
        return (
            <React.Fragment>
                <div>
                    <h2>the best photos make you feel something, share a special one with us</h2>
                </div>
                <div className="preview">
                    <div 
                        className="preview-image"
                        style={{
                            backgroundImage: `url(${this.state.file})`, 
                            border: this.state.file ? "none" : "1px dashed white" 
                        }}
                    >
                    </div>
                </div>
                <div className="upload-submit-container">
                    <form method="post" encType="multipart/form-data" onSubmit={this.handleSubmit}>
                        <input
                            id="file"
                            className="input-file"
                            ref={(ref) => { this.uploadInput = ref; }}
                            type="file" name="file"
                            accept="image/*"
                            onClick={this.props.onClick}
                            onChange={this.handleChange}
                        />
                        <label htmlFor="file" className="top-buttons blue big">CHOOSE IMAGE</label>
                    </form>
                    <button
                        className="confirm-button"
                        onClick={() => this.handleSubmit()}
                    >
                        CONFIRM
                    </button>
                </div>
                <p className="disclaimer"><em>*photos are submitted at-will and may appear in future vlush media</em></p>
            </React.Fragment>
        );
    }
}

export default ImageUpload;