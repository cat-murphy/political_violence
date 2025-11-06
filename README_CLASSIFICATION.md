# Political Violence Classification Script

This repository contains scripts to classify political violence events using Claude-4-Sonnet LLM as requested.

## Files

- `classification_script.py` - Main production script that processes all events
- `demo_classification.py` - Demo script with mock classification (for testing without API key)
- `test_classification.py` - Test script that processes only 5 events
- `us_data_filtered.csv` - Input data file with events to classify
- `green_11_5.csv` - Example events meeting political violence criteria
- `yellow_11_5.csv` - Example events for reference
- `us_data_enhanced.json` - Output file with classifications

## Setup

1. Install the required Python packages:
   ```bash
   pip install llm
   llm install llm-claude-3
   ```

2. Set up your Anthropic API key:
   ```bash
   llm keys set anthropic
   ```
   Enter your Anthropic API key when prompted.

## Usage

### Full Processing (Production)

To process all events in the dataset:

```bash
python classification_script.py
```

This will:
- Load all events from `us_data_filtered.csv`
- Use Claude-4-Sonnet to classify each event
- Save results to `us_data_enhanced.json`
- Save intermediate results every 50 events
- Display progress and summary statistics

### Demo/Testing

To test the script without using the LLM API:

```bash
python demo_classification.py
```

This uses a mock classification function to demonstrate the script structure without API calls.

To test with only 5 events using the real LLM:

```bash
python test_classification.py
```

## Classifications

The script adds seven new fields to each event:

### 1. attack_type
- **FIRE/EXPLOSIVE**: Events involving fire, bombs, explosives, IEDs, molotov cocktails
- **VEHICLE**: Vehicle ramming attacks
- **SHOOTING**: Events involving firearm discharge
- **ASSAULT WITH A WEAPON**: Physical assault using weapons (knives, hammers, etc.)
- **ASSAULT**: Physical assault without weapons
- **PROPERTY DESTRUCTION**: Events primarily involving destruction of buildings, statues, flags
- **OTHER**: Events not fitting other categories

### 2. extremist_beliefs_classification
- **YES**: Perpetrator associated with extremist beliefs (Nazism, white supremacy, religious extremism, etc.)
- **NO**: No association with extremist beliefs

### 3. connection_to_organized_extremist_group_classification
- **YES**: Perpetrator is member of organized extremist group
- **NO**: No connection to organized groups
- **N/A**: Set when extremist_beliefs_classification is "NO"

### 4. sole_perpetrator_classification
- **YES**: Perpetrator acted alone
- **NO**: Multiple attackers or unclear number of perpetrators

### 5. issue_type
- **ISRAEL/PALESTINE**: Israel/Palestine conflict related
- **COVID**: COVID-19 pandemic and related policies
- **REPRODUCTIVE AND WOMEN'S RIGHTS**: Reproductive rights, abortion issues
- **LGBTQ+ RIGHTS**: LGBTQ+ rights and related policies
- **IMMIGRATION**: Immigration and immigration policy
- **BLACK LIVES MATTER**: BLM movement and racial justice
- **HOMELESSNESS**: Homelessness and related policies
- **OTHER WORLD CONFLICT**: Other international conflicts
- **LABOR**: Labor issues, strikes, collective bargaining
- **ELECTIONS/VOTING/POLITICS**: Elections, voting, general politics
- **OTHER — CHECK MANUALLY**: Political motive but doesn't fit other categories

### 6. target
- **PUBLIC FIGURE**: Attacks on politicians, public officials, cultural figures
- **INSTITUTION**: Attacks on buildings, agencies, organizations, symbols
- **CIVILIANS**: Attacks on general public, crowds, identity-based groups

### 7. political_violence_classification
- **POLITICAL VIOLENCE**: Events with violent action and clear political motive
- **NOT POLITICAL VIOLENCE**: Events without violence or clear political motive

## Classification Hierarchy

The script follows this hierarchy for attack_type:
1. FIRE/EXPLOSIVE (highest priority)
2. VEHICLE 
3. SHOOTING
4. ASSAULT WITH A WEAPON
5. ASSAULT
6. PROPERTY DESTRUCTION
7. OTHER (lowest priority)

## Error Handling

- If the LLM cannot provide a confident classification, fields are set to "MANUAL CHECK"
- Intermediate results are saved every 50 events to prevent data loss
- Timeout protection prevents hanging on slow API calls

## Output Format

The output file `us_data_enhanced.json` contains:
- All original event data from the CSV
- Three new classification fields
- JSON format for easy parsing

## Monitoring Progress

The script displays:
- Current event being processed
- Percentage complete
- Summary statistics at completion
- Any errors or warnings

## Performance Notes

- Processing ~1,640 events takes approximately 30-60 minutes depending on API response times
- Costs approximately $15-30 in Anthropic API credits for full dataset
- Uses Claude-4-Sonnet model for high-quality classifications

## Troubleshooting

**API Key Issues:**
```bash
llm keys set anthropic
```

**Permission Issues:**
```bash
chmod +x classification_script.py
```

**Missing Dependencies:**
```bash
pip install llm
llm install llm-claude-3
```

**Check Available Models:**
```bash
llm models
```