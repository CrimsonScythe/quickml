import React from 'react';
import {connect} from 'react-redux'
import {uploadFile} from '../actions'

// import StreamForm from './StreamForm'

class FileUpload extends React.Component {
    
    state = {

    }

    onFileChange = (event) => {
        event.preventDefault()
        console.log('change')
        const f = event.target.value
        // this.props.setFile(f)
        this.setState({selectedFile: event.target.files[0]})
    }

    
    onFileUpload = () => {
      
        const formData = new FormData()
        formData.append('file', this.state.selectedFile)

        this.props.uploadFile(formData)
        
    }

    dropDown = () => {
        if (this.props.file['uploadresponse']){
        return(
            <div>
            <label htmlFor="preds">Predict: </label>
            <select name="preds" id="pred">
                <option value="volvo">Volvo</option>
                <option value="saab">Saab</option>
                <option value="mercedes">Mercedes</option>
                <option value="audi">Audi</option>
            </select>
            </div>
        )
    }
    }

    render() {
        console.log('rendered')
        console.log(this.props.file)
        return (
            <div>
                <h1>Hello World!</h1>
            <div> 
                <input type="file" onChange={this.onFileChange} /> 
                <button onClick={this.onFileUpload}> 
                  Upload! 
                </button> 
                {this.dropDown()}
            </div> 
            
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        file: state.files
    }
}

export default connect(mapStateToProps, {uploadFile}) (FileUpload)