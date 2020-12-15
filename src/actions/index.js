import axios from "axios"
import {
    FILE_SET,
    FILE_UPLOAD
} from './types'

export const uploadFile = (fileData) => {
    return async(dispatch, getState) => {

        const response = await axios.post('http://127.0.0.1:5000/post', fileData)

        dispatch({type: FILE_UPLOAD, payload: response.data})
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