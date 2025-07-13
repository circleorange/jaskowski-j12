# Overview

This repository contains the solution submitted by team J12 for the EURO/ROADEF
2012 Challange Machine Reassignment Problem proposed by Google:<br>
http://challenge.roadef.org/2012/en/index.php.

For more informations about the solution see:<br>
http://www.cs.put.poznan.pl/wjaskowski/projects/roadef-challenge-2012.

# Dependencies

- Java 8
- Ant
- IBM ILOG CPLEX Studio v22.1.1 (specifically for the MIP solver)

# Build

- To compile and build the build/roadef.jar file, run:
```
ant jar
```

Other `ant` commands include; `ant clean`, `ant compile`.

# Run

- As the project relies on CPLEX Solver v22.1.1, ensure it is accessible to the system:
```
export CPLEX_STUDIO=/opt/ibm/ILOG/CPLEX_Studio2211
export LD_LIBRARY_PATH=$CPLEX_STUDIO/cplex/bin/x86-64_linux:$LD_LIBRARY_PATH
```

- Run the project (using an example configuration `hc_lnshc.conf`):
```
java -jar build/jar/roadef.jar -conf conf/hc_lnshc.conf -p data/A/model_a1_2.txt -i data/A/assignment_a1_2.txt -o new_assignment_a1_2.txt -t 300
```
Alternatively, use the VS Code launch files.


# CPLEX v12.5 to v22.1.1 Compatibility Changes

The original solution used CPLEX Solver v12.5, however, official IBM website does not provide endpoints to download past releases - and only the latest, v22.1.1 is available (as of July 2025).

Hence the project is updated to comply with the new CPLEX engine interfaces.

## Summary
The ROADEF challenge solution has been successfully updated from CPLEX v12.5 (2012) to v22.1.1. The following compatibility issues were identified and resolved:

## Changes Made

### 1. Deprecated Method: setVectors()
**Issue**: The `cplex.setVectors()` method has been deprecated in CPLEX v22.1.1.
**Solution**: Replaced with `cplex.addMIPStart()` method.

**Before:**
```java
cplex.setVectors(vals, null, vars, null, null, null);
```

**After:**
```java
cplex.addMIPStart(vars, vals);
```

### 2. Deprecated Parameter API
**Issue**: The old parameter API using `IloCplex.IntParam.*` and `IloCplex.DoubleParam.*` has been deprecated.
**Solution**: Updated to use the new `IloCplex.Param.*` hierarchy.

**Key parameter updates:**
- `IloCplex.IntParam.Threads` → `IloCplex.Param.Threads`
- `IloCplex.DoubleParam.TiLim` → `IloCplex.Param.TimeLimit`
- `IloCplex.IntParam.NodeLim` → `IloCplex.Param.MIP.Limits.Nodes`
- `IloCplex.DoubleParam.EpAGap` → `IloCplex.Param.MIP.Tolerances.AbsMIPGap`
- `IloCplex.DoubleParam.EpGap` → `IloCplex.Param.MIP.Tolerances.MIPGap`
- `IloCplex.DoubleParam.CutUp` → `IloCplex.Param.MIP.Tolerances.UpperCutoff`
- `IloCplex.IntParam.MIPEmphasis` → `IloCplex.Param.Emphasis.MIP`

### 3. Removed Parameters
**Issue**: Some parameters from CPLEX v12.5 are no longer available in v22.1.1.
**Solution**: Commented out the following parameters that are no longer supported:
- `BarGrowth` (barrier growth parameter)
- `BarObjRng` (barrier objective range parameter)
- `ScaInd` (scaling indicator parameter)

## Notes
- `getNnodes64()` is deprecated but commented out in the code
- Some parameter settings that were specific to older CPLEX versions have been disabled but documented for reference
- The core functionality remains intact, just applied small adjustments for compatibility with the modern CPLEX API
