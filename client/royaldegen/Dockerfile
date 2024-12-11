FROM node:alpine as build

WORKDIR /app

COPY package.json package.json
RUN npm install
COPY . .
RUN npm build

FROM nginx:stable-alpine

RUN cp -rf dist/* /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5500

CMD ["nginx", "-g", "daemon off;"]
