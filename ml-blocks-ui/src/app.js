import axios from 'axios'
import Hierarchy from './tree'

function prase_children(obj) {
    if (obj.children) {
        obj.children = Object.values(obj.children)
    }

    obj.children.forEach(child => prase_children(child))
}

const host = 'http://localhost:9080'
// const host = ''

axios
    .get(`${host}/api/v1/pipe/graph`)
    .then(response => response.data)
    .then(data => {
        prase_children(data)
        // console.log(data)
        new Hierarchy(data)
    })

console.log('running!')