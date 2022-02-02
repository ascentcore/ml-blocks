import API from './API';

export const dataCount = async () => {
    return await API.get('/data/count');
}

export const getData = async () => {
    return await API.get('/data/');
}