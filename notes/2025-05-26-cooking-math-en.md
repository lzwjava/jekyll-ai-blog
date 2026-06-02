---
audio: false
generated: true
lang: en
layout: post
title: 'Cooking Math: Heat, Time, and Efficiency'
translated: false
type: note
---

Cooking involves several mathematical concepts and formulas that can help optimize recipes, portion sizes, and cooking processes. Below, I’ll introduce some key mathematical formulas and principles relevant to cooking, inspired by the provided cooking context. These formulas will focus on practical applications like scaling recipes, calculating cooking times, and managing heat transfer, while keeping the explanations concise and relatable to the cooking scenarios you mentioned (e.g., stir-frying, grilling, and soup-making).

---

### 1. **Scaling Recipes (Proportions and Ratios)**

When adjusting a recipe for a different number of servings, you use ratios to scale ingredients proportionally.

**Formula**:
\\[ \text{New Quantity} = \text{Original Quantity} \times \frac{\text{New Servings}}{\text{Original Servings}} \\]

**Example**:
If a stir-fry recipe for 4 servings calls for 200g of broccoli, but you’re cooking for 6 people:
\\[ \text{New Quantity} = 200 \times \frac{6}{4} = 300 \, \text{g of broccoli} \\]

**Application**:
This is useful when preparing dishes like the meat, vegetable, chili, garlic, and ginger stir-fry you mentioned. If you’re cooking for a larger group, scale each ingredient (e.g., meat, vegetables) proportionally to maintain flavor balance.

---

### 2. **Cooking Time Based on Ingredient Size (Surface Area to Volume Ratio)**

The size of ingredients affects cooking time because smaller pieces have a larger surface area relative to their volume, allowing faster heat transfer. This is why you mentioned cutting meat into small pieces for stir-frying.

**Formula (Surface Area to Volume Ratio for a Cube)**:
For a cube with side length \\( s \\):
\\[ \text{Surface Area} = 6s^2 \\]
\\[ \text{Volume} = s^3 \\]
\\[ \text{Ratio} = \frac{\text{Surface Area}}{\text{Volume}} = \frac{6s^2}{s^3} = \frac{6}{s} \\]

**Example**:
A potato cube with a side length of 2 cm has a surface area-to-volume ratio of \\( \frac{6}{2} = 3 \, \text{cm}^{-1} \\). If you cut it into 1 cm cubes, the ratio becomes \\( \frac{6}{1} = 6 \, \text{cm}^{-1} \\), doubling the relative surface area, so it cooks faster.

**Application**:
When using a vegetable chopper to cut potatoes or peppers into smaller pieces (as you mentioned), smaller cubes or strips cook faster in stir-fries or soups due to increased surface area for heat transfer.

---

### 3. **Heat Transfer and Cooking Time (Newton’s Law of Cooling/Heating)**

Cooking involves transferring heat to food, and the rate of heating depends on the temperature difference between the food and the heat source (e.g., oil for stir-frying or a grill oven at 200°C).

**Formula (Simplified Newton’s Law of Cooling/Heating)**:
\\[ \frac{dT}{dt} = -k (T - T_{\text{env}}) \\]
Where:

- \\( T \\): Temperature of the food
- \\( T_{\text{env}} \\): Temperature of the cooking environment (e.g., oil, oven)
- \\( k \\): Heat transfer coefficient (depends on the cooking method)
- \\( t \\): Time

For practical purposes, this implies that cooking time decreases as the temperature difference increases.

**Example**:
Stir-frying with oil (boiling point ~300°C) heats food faster than boiling in water (100°C) because oil provides a larger \\( T_{\text{env}} \\), as you noted. For a piece of meat to reach an internal temperature of 70°C, stir-frying in oil at 200°C will take less time than boiling.

**Application**:
This explains why broccoli requires more stir-frying time than mushrooms or meat (as you mentioned). Broccoli’s denser structure and higher water content result in a lower \\( k \\), slowing heat transfer.

---

### 4. **Dilution Formula for Seasoning (e.g., Salt or Soy Sauce)**

To avoid over-seasoning (like using too much salt with soy sauce, as you cautioned), you can calculate how much seasoning to add when diluting or concentrating a dish.

**Formula**:
\\[ C_1 V_1 = C_2 V_2 \\]
Where:

- \\( C_1 \\): Initial concentration of seasoning
- \\( V_1 \\): Initial volume
- \\( C_2 \\): Desired concentration
- \\( V_2 \\): Final volume

**Example**:
If you have 500 mL of soup with a salt concentration of 2% and want to dilute it to 1% by adding water:
\\[ 2\% \times 500 = 1\% \times V_2 \\]
\\[ V_2 = 1000 \, \text{mL} \\]
You need to add 500 mL of water to reach a 1% salt concentration.

**Application**:
This is useful when making Chinese yam soup or adjusting seasoning in a rice cooker dish to prevent over-salting, especially when ingredients like soy sauce are already used.

---

### 5. **Energy Consumption for Cooking Appliances**

To estimate the energy used by appliances like a grill oven or rice cooker, you can calculate power consumption.

**Formula**:
\\[ E = P \times t \\]
Where:

- \\( E \\): Energy (in watt-hours or Wh)
- \\( P \\): Power rating of the appliance (in watts)
- \\( t \\): Time (in hours)

**Example**:
A grill oven rated at 1000 W used for 20 minutes (as you mentioned for grilling meat at 200°C):
\\[ t = \frac{20}{60} = 0.333 \, \text{hours} \\]
\\[ E = 1000 \times 0.333 = 333 \, \text{Wh} \\]

**Application**:
This helps estimate the energy cost of using a grill oven for egg tarts or meat versus an electric cooker for soup, aiding in cost-effective cooking choices.

---

### 6. **Cooking Order and Timing (Linear Scheduling)**

When stir-frying ingredients with different cooking times (e.g., broccoli vs. mushrooms), you can model the process as a linear scheduling problem to minimize overcooking or undercooking.

**Formula (Basic Timing Model)**:
\\[ T_{\text{total}} = T_1 + T_2 + \dots + T_n \\]
Where \\( T_i \\) is the cooking time for each ingredient, added sequentially based on the order of addition.

**Example**:

- Broccoli: 5 minutes
- Mushrooms: 2 minutes
- Meat: 3 minutes
If you add broccoli first, then mushrooms after 3 minutes, and meat 1 minute later:
\\[ T_{\text{total}} = 5 \, \text{minutes (broccoli)} + 2 \, \text{minutes (mushrooms)} + 1 \, \text{minute (meat)} = 6 \, \text{minutes} \\]
This ensures all ingredients are cooked just right by staggering their addition.

**Application**:
As you noted, the order of adding ingredients matters in stir-frying to account for different cooking times, ensuring a balanced dish.

---

### 7. **Marination Absorption (Diffusion Approximation)**

Marinating ingredients (e.g., with cornflour, soy sauce, or fruit juice) involves diffusion, where flavors penetrate the food. The depth of penetration depends on time and ingredient size.

**Formula (Simplified Diffusion)**:
\\[ x = \sqrt{2Dt} \\]
Where:

- \\( x \\): Depth of marinade penetration
- \\( D \\): Diffusion coefficient (depends on the food and marinade)
- \\( t \\): Marination time

**Example**:
For meat cut into 1 cm cubes, a marinade like soy sauce might penetrate ~2 mm in 30 minutes (assuming \\( D \approx 10^{-10} \, \text{m}^2/\text{s} \\)). Smaller pieces marinate faster due to shorter diffusion distances.

**Application**:
This supports your advice to cut meat into small pieces for effective marination with soy sauce or fruit juice before grilling or stir-frying.

---

### Practical Notes

- **Tools and Efficiency**: Using a vegetable chopper or mortar and pestle (as you mentioned) reduces preparation time, which can be modeled as a time-saving optimization problem in cooking workflows.
- **Grill vs. Steamer**: Your point about grill ovens producing drier food aligns with heat transfer principles—grilling relies on conduction and radiation, while steaming uses convection with water, affecting moisture content.
- **Minimizing Pot Washing**: This can be approached as an optimization problem, grouping ingredients with similar cooking methods to reduce cleaning time, aligning with your programming analogy.

Would you like me to create a chart (e.g., comparing cooking times for different ingredients) or dive deeper into any specific formula with examples or calculations tailored to your cooking scenarios? For example, I could calculate exact ingredient ratios for a scaled-up stir-fry recipe or model the energy use of your grill oven.
