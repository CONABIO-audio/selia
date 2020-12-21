const initialState = {
    items: []
}

const itemsReducer = (state = initialState, action) => {
    switch (action.type) {
        case "ADD_ITEM":
            return {
                ...state,
                items: [...state.items, action.payload]
            };
        case "DELETE_ITEM":
            return {
                items: [
                    ...state.items.filter(item => item !== action.payload)
                ]
            };
        case "CHANGE_ITEM":
            return {
                items: state.items.map(item => item.file === action.payload.file ?
                    { ...item, selected: !action.payload.selected } : 
                    item 
                )
            }
        default:
            return state;
    }
}

export default itemsReducer;