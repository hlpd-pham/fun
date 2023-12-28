package main

import (
  "bufio"
  "flag"
  "fmt"
  "os"
  "errors"
  "strconv"
)

func main() {
  var inputFile string
  flag.StringVar(&inputFile, "i", "", "Specify the input filename")
  flag.StringVar(&inputFile, "input", "", "Specify the input filename")

  flag.Parse()

  if inputFile == "" {
    fmt.Println("Usage: go run part1.go -i/--input <filename>")
    return
  }

  file, err := os.Open(inputFile)
  if err != nil {
    fmt.Println("Error opening file:", err)
    return
  }
  defer file.Close()

  var lines []string

  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    line := scanner.Text()
    lines = append(lines, line)
  }

  solve(lines)

  if err := scanner.Err(); err != nil {
    fmt.Println("Error reading file:", err)
    return
  }
}

func solve(lines []string) error {
  var total = 0;
  for _, l := range lines {
    var startDigit int
    var endDigit int

    // get first digit
    for i := 0; i < len(l); i++ {
      if '0' <= l[i] && l[i] <= '9' {
        startDigit, _ = strconv.Atoi(l[i:i+1])
        break
      }
    }
    if startDigit == 0 {
      errorMessage := fmt.Sprintf("cannot find a digit from line: %s", l)
      return errors.New(errorMessage)
    }
    for i := len(l) - 1; i >= 0; i-- {
      if '0' <= l[i] && l[i] <= '9' {
        endDigit, _ = strconv.Atoi(l[i:i+1])
        break
      }
    }

    total += startDigit * 10 + endDigit
  }
  fmt.Println(total)
  return nil
}


