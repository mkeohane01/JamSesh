# Traditional Modeling
Because of the complex nature of implementing music generation without the use of generative models or other deep learning techniques, I did not implement it for this project. I will walk through a high-level pipeline for how one may implement such an application though.

## Traditional Jam Sesh approach

**Prompt Analysis:** Utilize keyword extraction techniques, such as bag of words, to analyze the input prompt and identify its music genre or mood.

**Database Mapping:** Maintain a database where chord progressions, scales, and example patterns are associated with specific genres / styles.

**Refinement:** Adjust and refine the selection, ensuring the musical coherence to the input style as well as add creative, random variations to patterns

**Key Mapping:** Make sure to transpose the pattern to the key specified by the user

## Thoughts

A method like this would require a lot of complicatations inlcuding first a populated database full of various musical examples. Then after the example is retrieved based on the query, there would need to be code to refine the music to fit other styles along with mixing up the patterns musically. Finally other methods would be implemented to fit the progressions to the key or instrumentation requested.