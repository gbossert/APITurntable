package sse

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
)

//SSE name constants
const (
	eName  = "event"
	dName  = "data"
	idName = "id"
)

var (
	//ErrNilChan will be returned by Notify if it is passed a nil channel
	ErrNilChan = fmt.Errorf("nil channel given")
)

//Client is the default client used for requests.
var Client = &http.Client{}

func liveReq(verb, uri string, body io.Reader) (*http.Request, error) {
	req, err := GetReq(verb, uri, body)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Accept", "text/event-stream")

	return req, nil
}

//Event is a go representation of an http server-sent event
type Event struct {
	URI  string
	Type string
	Data io.Reader
	ID   string
}

//GetReq is a function to return a single request. It will be used by notify to
//get a request and can be replaces if additional configuration is desired on
//the request. The "Accept" header will necessarily be overwritten.
var GetReq = func(verb, uri string, body io.Reader) (*http.Request, error) {
	return http.NewRequest(verb, uri, body)
}

//Notify takes the uri of an SSE stream and channel, and will send an Event
//down the channel when recieved, until the stream is closed. It will then
//close the stream. This is blocking, and so you will likely want to call this
//in a new goroutine (via `go Notify(..)`)
func Notify(uri string, evCh chan<- *Event) error {
	if evCh == nil {
		log.Fatal(ErrNilChan.Error())
		return ErrNilChan
	}

	req, err := liveReq("GET", uri, nil)
	if err != nil {
		return fmt.Errorf("error getting sse request: %v", err)
	}

	res, err := Client.Do(req)
	if err != nil {
		return fmt.Errorf("error performing request for %s: %v", uri, err)
	}

	br := bufio.NewReader(res.Body)
	defer res.Body.Close()

	delim := []byte{':', ' '}

	var currEvent *Event
	currEvent = &Event{URI: uri}

	for {
		bs, err := br.ReadBytes('\n')

		if err != nil && err != io.EOF {
			return err
		}

		if len(bs) < 2 {
			if currEvent.ID != "" && currEvent.Data != nil {
				evCh <- currEvent
				currEvent = &Event{URI: uri}
			}
			continue
		}

		spl := bytes.Split(bs, delim)

		if len(spl) < 2 {
			currEvent = &Event{URI: uri}
			continue
		}

		switch string(spl[0]) {
		case eName:
			currEvent.Type = string(bytes.TrimSpace(spl[1]))
		case dName:
			data := bytes.TrimPrefix(bs, []byte("data: "))
			currEvent.Data = bytes.NewBuffer(bytes.TrimSpace(data))
		case idName:
			currEvent.ID = string(bytes.TrimSpace(spl[1]))
		}
		if err == io.EOF {
			break
		}
	}
	return nil
}
