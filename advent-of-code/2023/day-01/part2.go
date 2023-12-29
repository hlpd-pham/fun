package main

import (
  "bufio"
  "flag"
  "fmt"
  "os"
  "errors"
  "strconv"
)

const (
  BAD_CANDIDATE = "BAD_CANDIDATE"
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

  if err := solve(lines); err != nil {
    fmt.Println("Error trying to solve:", err)
  }
  

  if err := scanner.Err(); err != nil {
    fmt.Println("Error reading file:", err)
    return
  }
}

// check if candidate is good and return the candidate word, then find the corresponding mapping
func getCandidate(line string, startIndex int) string {
  digitWords := map[string]int{
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
  }
  lineLength := len(line)
  for key, _ := range digitWords {
    if startIndex + len(key) - 1 < lineLength {
      digitWordCandidate := line[startIndex:startIndex+len(key)]
      if digitWordCandidate == key {
        return key
      }
    }
  }
  return BAD_CANDIDATE
}

func solve(lines []string) error {
  digitWords := map[string]int{
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
  }
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
      result := getCandidate(l, i)
      if result != BAD_CANDIDATE {
        startDigit = digitWords[result]
        break
      }
    }
    if startDigit == 0 {
      errorMessage := fmt.Sprintf("cannot find a digit from line: %s", l)
      return errors.New(errorMessage)
    }

    // get second digit
    for i := len(l) - 1; i >= 0; i-- {
      if '0' <= l[i] && l[i] <= '9' {
        endDigit, _ = strconv.Atoi(l[i:i+1])
        break
      }
      result := getCandidate(l, i)
      if result != BAD_CANDIDATE {
        endDigit = digitWords[result]
        break
      }
    }

    total += (startDigit * 10 + endDigit)
  }
  fmt.Println(total)
  return nil
}


