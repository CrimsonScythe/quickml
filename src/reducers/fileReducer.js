import {
    FILE_SET, FILE_UPLOAD
} from '../actions/types'

export default (state={}, action) => {
    switch (action.type) {
        case FILE_SET:
            return {...state, ['file']: action.payload}
        case FILE_UPLOAD:
            return {...state, ['uploadresponse']: action.payload}
        default:
            return state
    }
}