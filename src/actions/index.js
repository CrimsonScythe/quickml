
import {
    FILE_SET,
    FILE_UPLOAD,
    COLS_GET,
    MODEL_TRAIN,
    MODEL_PRED
} from './types'

export const uploadFile = (fileData) => {
    return async(dispatch, getState) => {

        const formData = new FormData()
        formData.append('file', fileData)

        const response = await fetch('http://127.0.0.1:5000/post/prep', {method: 'POST', body: formData, credentials: 'same-origin'})
        const rawres = await response.json()
        // const response = await axios.post('http://127.0.0.1:5000/post/prep',fileData, {withCredentials: true})
        // console.log('response')
        // console.log(response)
        // console.log(response.data)
        // response.data for axios
        dispatch({type: FILE_UPLOAD, payload: rawres})
    }
}

export const setFile = (file) => {
    // console.log('ss')
    // console.log(file)
    return (dispatch) => {
        // const response = await axios.post('', )
        const f = file
        dispatch({type: FILE_SET, payload: f})
    }
}

export const getCols = () => {
    return async(dispatch, getState) => {

        const response = await fetch('http://127.0.0.1:5000/get/cols', {method: 'GET', credentials: 'same-origin'})
        // const response = await axios.get('http://127.0.0.1:5000/get/cols', {withCredentials: true})
        dispatch({type: COLS_GET, payload: response})
    }
}

export const trainModel = (column, selectedFile) => {
    return async(dispatch, getState) => {
     
        // const formData = new FormData()
        // formData.append('column_name', column)
     

        const formData = new FormData()
        formData.append('column_name', column)
        formData.append('file', selectedFile)
        

        const response = await fetch('http://127.0.0.1:5000/post/train', {method: 'POST', body: formData, credentials: 'same-origin'})

        // const response = await axios.post('http://127.0.0.1:5000/post/train', {column_name: column}, {withCredentials: true})
        dispatch({type: MODEL_TRAIN, payload: response})
    }
}

export const predModel = (column, selectedFile) => {
    return async(dispatch, getState) => {

        const formData = new FormData()
        formData.append('column_name', column)
        formData.append('file', selectedFile)
        

        const response = await fetch('http://127.0.0.1:5000/post/pred', {method: 'POST', body: formData, credentials: 'same-origin'})

        // const response = await axios.post('http://127.0.0.1:5000/post/train', {column_name: column}, {withCredentials: true})
        dispatch({type: MODEL_PRED, payload: response})

    }
}