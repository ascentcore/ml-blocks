import React, { useEffect, useState } from 'react';
import * as getValue from '../api/data';
import { makeStyles } from '@mui/styles';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, TableFooter } from '@mui/material';

const useStyles = makeStyles(() => ({
    paper: {
        marginTop: '60px',
        width: '100%',
        overflow: 'hidden',

    },
    tableContainer: {
        backgroundColor: '#F3F6F4',
    },
    tableFooter: {
        '& tr > td': {
            border: 0
        }
    }
}))

const DataScreen = () => {
    const classes = useStyles();
    const [value, setValue] = useState();
    useEffect(async () => {
        const response = await getValue.getData()
        setValue(response);
    }, []);

    const [count, setCount] = useState();

    useEffect(async () => {
        const response = await getValue.dataCount()
        setCount(response);
    }, [count]);

    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(5);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    return (
        <Paper className={classes.paper}>
            <TableContainer className={classes.tableContainer}>
                <Table  >
                    <TableBody>
                        {value?.data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, index) => (
                            <TableRow hover key={row}>
                                <TableCell component="th" scope="row">{row[0]}</TableCell>
                                <TableCell align="right">{row[1]}</TableCell>
                                <TableCell align="right">{row[2]}</TableCell>
                                <TableCell align="right">{row[3]}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                    <TableFooter className={classes.tableFooter}>
                        <TableRow align="right">
                            <TablePagination
                                rowsPerPageOptions={[5, 10, 50]}
                                count={count?.data[0]}
                                rowsPerPage={rowsPerPage}
                                page={page}
                                onPageChange={handleChangePage}
                                onRowsPerPageChange={handleChangeRowsPerPage}
                            />
                        </TableRow>
                    </TableFooter>
                </Table>
            </TableContainer>
        </Paper>
    )
}

export default DataScreen;