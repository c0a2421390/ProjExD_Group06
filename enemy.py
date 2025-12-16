import os
import random
from typing import Optional, Tuple

import pygame

__all__ = ["Enemy"]


class Enemy:
	"""敵キャラの基本クラス。

	Base.py からインスタンス化して使えるように、座標・体力・速度・描画処理を提供します。
	プレイヤー位置が渡されれば追跡し、渡されなければランダム歩行します。
	"""

	def __init__(
		self,
		x: int,
		y: int,
		hp: int = 10,
		speed: float = 1.0,
		image_path: Optional[str] = None,
		tile_size: int = 16,
	) -> None:
		
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = hp
		self.speed = speed
		self.tile_size = tile_size

		self._vx = 0.0
		self._vy = 0.0

		self._image = None
		self._rect = pygame.Rect(int(x), int(y), tile_size, tile_size)

		# 画像の読み込み（省略可）
		if image_path:
			try:
				base_dir = os.path.dirname(os.path.abspath(__file__))
				full_path = (
					image_path
					if os.path.isabs(image_path)
					else os.path.join(base_dir, image_path)
				)
				img = pygame.image.load(full_path).convert_alpha()
				self._image = pygame.transform.scale(img, (tile_size, tile_size))
			except Exception:
				# 読み込み失敗時は None のままにしてフォールバック描画を行う
				self._image = None

		# ランダム移動のためのタイマー
		self._change_dir_timer = 0.0

	def draw(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0) -> None:
		"""敵を描画する。カメラオフセットに対応。"""
		screen_x = int(self.x) - camera_x
		screen_y = int(self.y) - camera_y

		if self._image:
			surface.blit(self._image, (screen_x, screen_y))
		else:
			# フォールバック: シンプルな矩形
			pygame.draw.rect(
				surface,
				(200, 50, 50),
				(screen_x, screen_y, self.tile_size, self.tile_size),
			)
		
	@property
	def rect(self) -> pygame.Rect:
		return self._rect

