import { configureStore } from '@reduxjs/toolkit';
import itemsReducer from './features/itemReducer';

export default configureStore({
  reducer: {
    items: itemsReducer,
  },
});
