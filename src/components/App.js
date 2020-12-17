import React from 'react'
import FileUpload from './FileUpload'
import { Router, Route, Switch} from 'react-router-dom';
import Header from './Header'
import history from './history'

const App = () => {
    return(
        <div className="ui container">
            <Router history={history}>
                <div>
                    <Header/>
                    <Switch>
                    <Route path="/" exact component={FileUpload}></Route>
                    </Switch>
                </div>
            </Router>
        </div>
    )
    // state = {
    //     selectedFile: null
    // }

    // onFileChange = (event) => {
    //     event.preventDefault()
    //     console.log('change')
    //     this.setState({selectedFile: event.target.files[0]})
    // }

    // onFileUpload = async () => {
    //     console.log(this.state.selectedFile.name)
    //     const formData = new FormData()
    //     let file = this.state.selectedFile
    //     formData.append('file', file)
    //     await axios.post('http://127.0.0.1:5000/post', formData)
    // }

    // render() {
    //     return (
    //         <div>
    //             <h1>Hello World!</h1>
    //         <div> 
    //             <input type="file" onChange={this.onFileChange} /> 
    //             <button onClick={this.onFileUpload}> 
    //               Upload! 
    //             </button> 
    //         </div> 
    //         </div>
    //     )
    // }
}

export default App