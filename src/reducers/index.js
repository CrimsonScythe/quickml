import { combineReducers} from 'redux'
// import { reducer as formReducer} from 'redux-form'
// import authReducer from './authReducer'
// import streamReducer from './streamReducer'
import fileReducer from './fileReducer'

export default combineReducers({
    // auth: authReducer,
    // form: formReducer, //reducer provided by reduxform,
    // streams: streamReducer
    files: fileReducer
})
