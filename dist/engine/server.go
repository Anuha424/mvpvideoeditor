package main

import (
	"context"
	"net/http"
)

type httpServer struct {
	addr    string
	handler http.Handler
	srv     *http.Server
}

func (s *httpServer) listenAndServe() error {
	s.srv = &http.Server{Addr: s.addr, Handler: s.handler}
	return s.srv.ListenAndServe()
}

func (s *httpServer) shutdown(ctx context.Context) {
	if s.srv != nil {
		_ = s.srv.Shutdown(ctx)
	}
}
