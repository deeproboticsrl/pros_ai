**NOTE - FOR NOW DISTANCES ARE ONLY USED FOR GETTING THE START POINT. THEN EACH TRAJECTORY IS SAMPLED INDEPENDENT OF
OTHERS**

# Min distance images for all 3 normalisations

## Using body translational and rotational positions and misc positions

Expert indices
1. No norm - 15
2. Max norm - 65
3. Gaussian norm - 65

2 and 3 found the same expert - *subject20_Run_20001_cycle3_states*

while expert for 1 is *subject01_Run_20002_cycle2_states*

**1. No norm**

**Side view**

![image](https://user-images.githubusercontent.com/27682820/46909793-b0ca0700-cf55-11e8-816b-7053d1ff063b.png)

**Top view**

![image](https://user-images.githubusercontent.com/27682820/46911715-ec7ac600-cf81-11e8-803a-963e3a4faf94.png)

**2. Divide by max**

![image](https://user-images.githubusercontent.com/27682820/46909794-b7587e80-cf55-11e8-8029-3acf7669d682.png)

**3. (x - mean) / std** Same expert as above so here showing it's top view

![image](https://user-images.githubusercontent.com/27682820/46911706-91e16a00-cf81-11e8-9ae7-f34a49e7691d.png)

## Using body rotational positions

no and gaussian got expert 15 same as no when taking all pos

max found a different expert - index 94 *subject02_Run_20002_cycle3_states*

**Side view**

![image](https://user-images.githubusercontent.com/27682820/46911681-239ca780-cf81-11e8-89ef-1b21d4ce62f4.png)

**Top view**

![image](https://user-images.githubusercontent.com/27682820/46911700-74ac9b80-cf81-11e8-9df3-75bc6123d284.png)

## Using body translatinal and misc positions

No norm gave expert 65 same as max and gaussian when all positions were taken.

Max and gaussian found a different expert - 114 - subject20_Run_20001_cycle1_states

Although note that their indices differ a bit (581 for max and 584 for gaussian) Images below are for gaussian

**Side view**

![image](https://user-images.githubusercontent.com/27682820/46912077-8e9eac00-cf8a-11e8-85b1-3380cb85f0b5.png)

**Top view**

![image](https://user-images.githubusercontent.com/27682820/46912084-bbeb5a00-cf8a-11e8-8a12-2f7b5933074f.png)

## Using body translatinal and misc positions without toe, talus and pros_foot (minimal_TM)

Max and no - expert 114

Gaussian - expert 65

**Side view of max**

![image](https://user-images.githubusercontent.com/27682820/46912543-50f35080-cf95-11e8-80f4-93fbd9a8e5b9.png)


