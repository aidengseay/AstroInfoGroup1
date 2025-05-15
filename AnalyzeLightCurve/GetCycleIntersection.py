

# get the ids that intersect
print("finding intersecting asteroids...")
cycle1_df_unique = np.unique(cycle1_df["Original_Object_ID"])
cycle2_df_unique = np.unique(cycle2_df["Object_ID"])
intersect_ids_df = np.intersect1d(cycle1_df_unique, cycle2_df_unique)

columns = ["asteroid_id", "period_(hr)_1", "amplitude_1",    
               "period_(hr)_2", "amplitude_2"]