import React from 'react';

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
                <input ref={(ref) => { this.uploadInput = ref; }} type="file" name="file" accept="image/*" />
                <input type="submit" value="Upload" />
            </form>
        );
    }
}

export default ImageUpload;