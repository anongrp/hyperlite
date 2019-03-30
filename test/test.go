package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

func main() {
	data, err := ioutil.ReadFile("test/test.json")

	if err != nil {
	  fmt.Print(err)
	}

	//fmt.Println(data)

	type DummyDelete struct {
      name string
      email string
    }

	var obj DummyDelete

	err = json.Unmarshal(data, &obj)
    if err != nil {
        fmt.Println("error:", err)
    }

	fmt.Println(obj)
}
