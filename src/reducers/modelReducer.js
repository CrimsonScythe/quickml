import {
    FILE_SET, FILE_UPLOAD, COLS_GET, MODEL_TRAIN
} from '../actions/types'

export default (state={}, action) => {
    switch (action.type) {
        case MODEL_TRAIN:
            return {...state, ['modeltrainresponse']: action.payload}
        default:
            return state
    }
}