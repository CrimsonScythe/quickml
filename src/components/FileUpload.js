import React from 'react';
import {connect} from 'react-redux'
import {getCols, uploadFile, trainModel, predModel} from '../actions'

// import StreamForm from './StreamForm'

class FileUpload extends React.Component {
    
    state = {

    }

    onFileChange = (event) => {
        event.preventDefault()
        console.log('change')
      
        this.setState({selectedFile: event.target.files[0]})
    }

    
    onFileUpload = () => {
      
        

        this.props.uploadFile(this.state.selectedFile)
        
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
       
            this.props.trainModel(this.state.dropselected, this.state.selectedFile)
        }
    }

    onPredict = () => {
        this.props.predModel(this.state.dropselected, this.state.selectedFile)
    }

    modelPredict = () => {

        if (this.props.model['modeltrainresponse']) {
            return (
                <button onClick={this.onPredict}>PREDICT!</button>
            )
        }
    }

    results = () => {
        if (this.props.model['modelpredresponse']) {
            console.log('PREDICTIONS:')
            console.log(this.props.model['modelpredresponse'])
        }
    }

    render() {
        
        return (
            <div>
                <h1>Hello World!</h1>
            <div> 
                <input type="file" onChange={this.onFileChange} /> 
                <button onClick={this.onFileUpload}> Upload! </button> 
                {this.dropDown()}
                <div></div>
                <button onClick={this.onTrain}> Train! </button>
                <div></div>
                {this.modelPredict()}
                <div></div>
                {this.results()}
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

export default connect(mapStateToProps, {uploadFile, getCols, trainModel, predModel}) (FileUpload)