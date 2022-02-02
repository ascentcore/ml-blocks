import React, { useEffect, useState } from 'react';
import * as getValue from '../api/data';
import { DataGrid } from '@mui/x-data-grid';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, TableFooter } from '@mui/material';

const DataScreen = () => {
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
        <>
            <Paper sx={{ width: '100%', overflow: 'hidden' }} style={{ marginTop: '60px' }}>
                <TableContainer >
                    <Table sx={{ minWidth: 650 }} aria-label="simple table" >
                        <TableBody>
                            {value?.data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, index) => (
                                <TableRow
                                    key={row}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">{row[0]}</TableCell>
                                    <TableCell align="right">{row[1]}</TableCell>
                                    <TableCell align="right">{row[2]}</TableCell>
                                    <TableCell align="right">{row[3]}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                        <TableFooter>
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
        </>
    )
}

export default DataScreen;