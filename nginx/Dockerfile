FROM nginx

#remove the default nginx configuration
RUN rm  /etc/nginx/conf.d/default.conf

#replace with our own configuration
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
