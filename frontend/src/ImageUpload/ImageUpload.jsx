import React from 'react';
import './styles.css';

class ImageUpload extends React.Component {
    constructor(props) {
        super(props);
    
        // this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    state = {
        uploading: false,
        images: [],
        value: null
    }
    
    handleSubmit(e) {
        e.preventDefault();

        const files = this.uploadInput.files;

        this.setState({ uploading: true })
        const data = new FormData();
        data.append('file', files[0]);
    
        fetch('/api/v1/upload', {
            method: 'POST',
            body: data
        })
        .then(response => { 
            response.json().then((body) => {
                this.setState({ uploading: false });
            });
        })
    }
    
    render() {
        return (
            <form method="post" encType="multipart/form-data" onSubmit={this.handleSubmit}>
                <input
                    id="file"
                    className="input-file"
                    ref={(ref) => { this.uploadInput = ref; }}
                    type="file" name="file"
                    accept="image/*"
                    onClick={this.props.onClick}
                    onChange={this.handleSubmit}
                />
                <label htmlFor="file" className="top-buttons blue" id="left-button">BET</label>
            </form>
        );
    }
}

export default ImageUpload;