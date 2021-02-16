import { atom } from 'jotai';

export const argsAtom = atom({});
export const errorMessageAtom = atom({status: false, message: ''});
export const currentDivAtom = atom('preview');