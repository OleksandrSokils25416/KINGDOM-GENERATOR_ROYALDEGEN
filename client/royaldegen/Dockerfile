FROM node:alpine as build

COPY package.json package.json
RUN npm install
COPY . .
RUN npm build

FROM nginx:stable-alpine

COPY --from=build /dist /user/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5500

CMD["nginx", "-g", "daemon off;"]
