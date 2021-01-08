export const addItem = item => ({
    type: "ADD_ITEM",
    payload: item
})

export const deleteItem = item => ({
    type: "DELETE_ITEM",
    payload: item
})

export const changeItem = item => ({
    type: "CHANGE_ITEM",
    payload: item
})

export const changeStatus = item => ({
    type: "CHANGE_STATUS",
    payload: item
})