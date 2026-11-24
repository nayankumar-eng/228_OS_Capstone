# Test Cases

| ID | Module | Test Input | Expected Result |
|----|--------|------------|-----------------|
| T01 | Menu | 1 | CPU module opens |
| T02 | CPU | 8 4 9 5 2 | Scheduling results displayed |
| T03 | CPU | Quantum = 0 | Input error displayed |
| T04 | Memory | 100 500 200 300 600 | Allocation results displayed |
| T05 | Memory | -10 20 | Validation error |
| T06 | Deadlock | Valid matrices | SAFE/UNSAFE result |
| T07 | Deadlock | Allocation > Maximum | Error displayed |
| T08 | Disk | 98 183 37 122 14 124 65 67 | Disk results displayed |
| T09 | Input | abc | Input error |
| T10 | Bash | Menu option 5 | Bash system information displayed |
| T11 | Reports | Menu option 6 | CSV reports generated |
| T12 | Boundary | One process | Correct result |
| T13 | Boundary | One disk request | Correct movement |
| T14 | Menu | 99 | Invalid menu message |
