import React from 'react';
import schema from './upload-schema.json';
import { SchemaForm } from '@ascentcore/react-schema-form';
import { MUICheckbox } from './Components/MUICheckbox';
import MUIWrapper from './Components/MUIWrapper';
import { MUISubmit } from './Components/MUISubmit';
import { MUIChooseFile } from './Components/MUIChooseFile';
import { MUIAddButton } from './Components/MUIAddButton';
import { MUIRemoveButton } from './Components/MUIRemoveButton';

export default function Upload() {
    function onSubmit(data, errors) {
        if (!errors || !errors.length) {
            console.log(data)
        }
    }

    const customRegistry = {
        button: { component: MUISubmit, wrapper: MUIWrapper },
        boolean: { component: MUICheckbox, wrapper: MUIWrapper },
        file: { component: MUIChooseFile, wrapper: MUIWrapper },
        addButton: { component: MUIAddButton, wrapper: MUIWrapper },
        removeButton: { component: MUIRemoveButton, wrapper: MUIWrapper }
    }

    return (
        <SchemaForm
            schema={schema}
            onSubmit={onSubmit}
            config={{ registry: customRegistry }}
        />
    )
}