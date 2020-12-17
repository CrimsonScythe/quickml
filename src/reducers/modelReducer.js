import {
   MODEL_TRAIN, MODEL_PRED
} from '../actions/types'

export default (state={}, action) => {
 
    switch (action.type) {
        case MODEL_TRAIN:
            return {...state, ['modeltrainresponse']: action.payload}
        case MODEL_PRED:
            return {...state, ['modelpredresponse']: action.payload}
        default:
            return state
    }
}