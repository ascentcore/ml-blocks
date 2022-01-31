import { makeStyles } from "@mui/styles";

export const useStyles = makeStyles((theme) => ({
    input: {
        width: '200px',
        height: '60px',
    },
    slider: {
        marginLeft: '20px',
    },
    map: {
        height: '200px',
        width: '500px'
    },
    addButton: {
        height: '18px',
        position: 'sticky',
        marginTop: '10px',
    },
    selector: {
        height: '20px',
        marginLeft: '10px',
    },
    grid: {
        margin: ' 20px 0'
    },
    title: {
        marginRight: '10px',
    },
    radioButton: {
        marginLeft: '20px'
    },
    error: {
        color: 'red'
    },
    removeButton: {
        background: 'transparent',
        border: '1px solid red',
        color: 'red',
        width: '80px',
        height: '40px',
        '&:hover': {
            border: '1px solid red',
        },
    },
    chooseFile: {
        color: 'black',
        '&:hover': {
            backgroundColor: 'transparent',
        },
    }
}))