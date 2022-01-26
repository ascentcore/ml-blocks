import { makeStyles } from "@mui/styles";

export const useStyles = makeStyles((theme) => ({
    input: {
        width: '200px',
        height: '100px',
    },
    slider: {
        width: '500px'
    },
    map: {
        height: '200px',
        width: '700px'
    },
    addButton: {
        height: '15px',
        position: 'fixed',
        margin: '-15px 0 0 110px'
    },
    selector: {
        height: '20px',
        marginLeft: '10px'
    },
    grid: {
        margin: '20px 0'
    }
}))