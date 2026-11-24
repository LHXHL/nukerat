package capabilities

import "stageless/utils/tasks"

func WriteMsg(msg string) []byte {
	// Returns the message as bytes when it fits the worker buffer
	if len(msg) > tasks.ThreadBufferContent {
		return nil
	}
	return []byte(msg)
}
