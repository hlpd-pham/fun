## Calculate budget for each creator based on a set budget and distribution

### Sample input
```json
{
  "budget": 100,
  "distribution": {
    "Solarbacca": 0.1,
    "ThePrimeagen": 0.4,
    "Alesso": 0.5
  }
}
```

### Sample run
```bash
$ python runner.py -i input.json
Budget: $100
Creator: Solarbacca, budget: $10.00
Creator: ThePrimeagen, budget: $40.00
Creator: Alesso, budget: $50.00
```
