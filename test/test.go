package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

func main() {
	data, err := ioutil.ReadFile("test/dummy_delete.json")

	if err != nil {
	  fmt.Print(err)
	}

	//fmt.Println(data)

	type DummyDelete struct {
      Delete interface{}
    }

	var obj DummyDelete

	err = json.Unmarshal(data, &obj)
    if err != nil {
        fmt.Println("error:", err)
    }

	fmt.Println(obj)

	obj1 := obj.Delete
	fmt.Println(obj1)
}
