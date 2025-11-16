def rotate_piece(piece_dict, angle_deg):
    rotated_piece = piece_dict.copy()
    
    portes_originales = piece_dict.get("porte", {})
    if portes_originales is None:
        portes_originales = {}
    
    portes_rotatives = {}
    rotation_map = {}
    
    if angle_deg == 90: 
        rotation_map = {"N": "O", "O": "S", "S": "E", "E": "N"}
    elif angle_deg == 180: 
        rotation_map = {"N": "S", "S": "N", "E": "O", "O": "E"}
    elif angle_deg == 270: 
        rotation_map = {"N": "E", "E": "S", "S": "O", "O": "N"}
    else: 
        rotated_piece["rotation_angle"] = 0
        return rotated_piece 
    
    for old_dir, new_dir in rotation_map.items():
        portes_rotatives[new_dir] = portes_originales.get(old_dir, False)
        
    rotated_piece["porte"] = portes_rotatives
    rotated_piece["rotation_angle"] = angle_deg

    img_original_scaled = rotated_piece.get("image_original")
    
    if img_original_scaled:
        rotated_img = pygame.transform.rotate(img_original_scaled, angle_deg)
        final_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        dest_center = (TILE_SIZE // 2, TILE_SIZE // 2)
        rotated_rect = rotated_img.get_rect(center = dest_center)
        final_surface.blit(rotated_img, rotated_rect)
        rotated_piece["image"] = final_surface
        
    return rotated_piece


def in_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS