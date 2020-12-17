import React from 'react';
import {connect} from 'react-redux'
import {getCols, uploadFile, trainModel} from '../actions'

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

    onDropSelect = (event) => {
        this.setState({dropselected: event.target.value})
    }

    dropDown = () => {

        // console.log(this.props.file['cols'])
        // console.log('up response')
        // console.log(this.props.file['uploadresponse'])
        if (this.props.file['uploadresponse']){
        let buildList = this.props.file['uploadresponse'].map((index, ite) => <option key={ite} value={index}>{index}</option>)
            
            // console.log('calling')
            // this.props.getCols()
        return(
            <div>
            <label htmlFor="preds">Predict: </label>
            <select name="preds" onChange={this.onDropSelect} id="pred">
                {buildList}
            </select>
            </div>
        )
    }
    }

    onTrain = () => {
        if (this.state.dropselected) {
            console.log(this.state.dropselected)
            this.props.trainModel(this.state.dropselected)
        }
    }

    modelPredict = () => {
        if (this.state.model) {
            return (
                <button>PREDICT!</button>
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
                <button onClick={this.onFileUpload}> Upload! </button> 
                {this.dropDown()}
                <button onClick={this.onTrain}> Train! </button>
                {this.modelPredict}
            </div> 
            
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        file: state.files,
        model: state.model
    }
}

export default connect(mapStateToProps, {uploadFile, getCols, trainModel}) (FileUpload)